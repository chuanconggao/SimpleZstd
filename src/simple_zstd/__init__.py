from zstandard import (
    ZstdCompressionDict,
    ZstdCompressor,
    ZstdDecompressor,
    train_dictionary,
)

# Dict size of 128 KB
_DICT_SIZE: int = 128 * 1_024

# Must have enough samples to train dict
# Otherwise, zstd complains with error: `cannot train dict: Src size is incorrect`
_MIN_SAMPLE_SIZE: int = 10


class Session:
    def __init__(self) -> None:
        self.__samples: list[bytes] = []
        self.__dict: ZstdCompressionDict | None = None

        self.__compressor: ZstdCompressor | None = None
        self.__decompressor: ZstdDecompressor | None = None

    def __train(self, data: bytes) -> None:
        self.__samples.append(data)

        if len(self.__samples) >= _MIN_SAMPLE_SIZE:
            self.__dict = train_dictionary(
                dict_size=_DICT_SIZE,
                samples=self.__samples,
                # Enable all error message details
                # notifications=4,
            )

            self.__compressor = None
            self.__decompressor = None

    def compress(self, data: bytes) -> bytes:
        if not self.__dict:
            self.__train(data)

        if not self.__compressor:
            self.__compressor = ZstdCompressor(
                dict_data=self.__dict,
            )

        return self.__compressor.compress(data)

    def decompress(self, data: bytes) -> bytes:
        if not self.__decompressor:
            self.__decompressor = ZstdDecompressor(
                dict_data=self.__dict,
            )

        result: bytes = self.__decompressor.decompress(data)

        if not self.__dict:
            self.__train(result)

        return result


__DEFAULT_SESSION = Session()


def compress(data: bytes) -> bytes:
    return __DEFAULT_SESSION.compress(data)


def decompress(data: bytes) -> bytes:
    return __DEFAULT_SESSION.decompress(data)
