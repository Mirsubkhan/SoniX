from typing import Callable, Awaitable

STTCallback = Callable[[int], Awaitable[None]]
DynamicSSTCallback = Callable[[str, bool], Awaitable[None]]
SeparatorProgressCallback = Callable[[int], Awaitable[None]]
