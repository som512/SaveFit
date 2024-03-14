import json
import os
import threading
import time
from threading import Event
from typing import Any, Dict, List

import numpy as np
from sora_sdk import (
    Sora,
    SoraAudioSink,
    SoraAudioSource,
    SoraConnection,
    SoraSignalingErrorCode,
    SoraTrackInterface,
    SoraVideoSink,
    SoraVideoSource,
)


class Sendrecv:
    def __init__(self, signaling_urls: list[str], channel_id: str):
        # シグナリング URL、ロール、チャネル ID を初期化
        self._signaling_urls: List[str] = signaling_urls
        self._channel_id: str = channel_id

        self._role: str = "sendrecv"

        self.connection_id: str

        self._connected: Event = Event()
        self._closed: bool = False

        self._video_height: int = 480
        self._video_width: int = 640

        # Sora インスタンスの生成
        self._sora: Sora = Sora()

        self._audio_source: SoraAudioSource = self._sora.create_audio_source(
            sample_rate=48000, channels=1
        )
        self._video_source: SoraVideoSource = self._sora.create_video_source()

        # Sora への接続設定
        self._connection: SoraConnection = self._sora.create_connection(
            signaling_urls=self._signaling_urls,
            role=self._role,
            channel_id=self._channel_id,
            # create_connection するタイミングで audio_source と video_source を指定する
            audio_source=self._audio_source,
            video_source=self._video_source,
        )

        # コールバックの登録
        self._connection.on_set_offer = self._on_set_offer
        self._connection.on_notify = self._on_notify
        self._connection.on_disconnect = self._on_disconnect

    def connect(self):
        # Sora へ接続
        self._connection.connect()

        self._audio_input_thread = threading.Thread(
            target=self._audio_input_loop, daemon=True
        )
        self._audio_input_thread.start()

        self._video_input_thread = threading.Thread(
            target=self._video_input_loop, daemon=True
        )
        self._video_input_thread.start()

        # 接続完了まで待機
        assert self._connected.wait(10), "接続に失敗しました"

        return self

    # ダミー音声
    def _audio_input_loop(self):
        # パラメータ
        sample_rate = 16000  # サンプリングレート (Hz)
        freq = 440  # 周波数 (Hz)
        duration = 0.02  # 時間 (秒)
        amplitude = 0.25  # 振幅

        # 時間配列を生成
        t = np.arange(int(sample_rate * duration)) / sample_rate

        while not self._closed:
            # sin 波を生成
            sin_wave = np.sin(2 * np.pi * freq * t)

            # sin 波を 16 ビット整数に変換
            sin_wave_int16 = np.int16(sin_wave * 32767 * amplitude)

            # sin 波を送信
            self._audio_source.on_data(sin_wave_int16.reshape(-1, 1))

            # 次のサイクルのために時間を進める
            t += duration

    # ダミー映像
    def _video_input_loop(self):
        while not self._closed:
            time.sleep(1.0 / 30)
            self._video_source.on_captured(
                np.zeros((self._video_height, self._video_width, 3), dtype=np.uint8)
            )

    def disconnect(self):
        # Sora から切断
        self._connection.disconnect()
        # スレッドの終了を待機
        self._audio_input_thread.join(10)
        self._video_input_thread.join(10)

    def _on_notify(self, raw_message: str):
        # シグナリング通知のコールバック
        message = json.loads(raw_message)
        # event_type が connection.created で、
        # connection_id が自分の connection_id と一致する場合、接続が成功
        if (
            message["type"] == "notify"
            and message["event_type"] == "connection.created"
            and message["connection_id"] == self.connection_id
        ):
            print(f"Sora に接続しました: connection_id={self.connection_id}")
            # 接続が成功したら connected をセット
            self._connected.set()

    def _on_set_offer(self, raw_message: str):
        # シグナリング type: offer のコールバック
        message = json.loads(raw_message)
        # "type": "offer" に自分の connection_id が入ってくるので取得しておく
        if message["type"] == "offer":
            self.connection_id = message["connection_id"]

    def _on_disconnect(self, error_code: SoraSignalingErrorCode, message: str):
        # 切断時のコールバック
        print(f"Sora から切断されました: error_code={error_code}, message={message}")
        self._closed = True
        # 切断完了で connected をクリア
        self._connected.clear()

    def _on_track(self, track: SoraTrackInterface):
        # トラック受信時のコールバック
        if track.kind == "audio":
            self._audio_sink = SoraAudioSink(
                track=track, output_frequency=16000, output_channels=1
            )

        if track.kind == "video":
            self._video_sink = SoraVideoSink(track=track)

    def run(self):
        try:
            # 接続を維持
            while not self._closed:
                pass
        except KeyboardInterrupt:
            # キーボード割り込みの場合
            pass
        finally:
            # 接続の切断
            if self._connection:
                self._connection.disconnect()


def main():
    # 環境変数からシグナリング URL とチャネル ID を取得
    signaling_url = os.getenv("SORA_SIGNALING_URL")
    channel_id = os.getenv("SORA_CHANNEL_ID")
    # signaling_url はリストである必要があるため、リストに変換
    signaling_urls = [signaling_url]

    # Sendrecv インスタンスの生成
    sample = Sendrecv(signaling_urls, channel_id)

    # Sora へ接続
    sample.connect()

    time.sleep(3)

    sample.disconnect()

    # 接続の維持する場合は sample.disconnect() の代わりに sample.run() を呼ぶ
    # sample.run()


if __name__ == "__main__":
    main()