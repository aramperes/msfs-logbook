import datetime
import struct
import sys
from io import BytesIO


class Buf:
    def __init__(self, buf: BytesIO):
        self._buf = buf
        self._order = 'little'

    def read_i8(self):
        return int.from_bytes(self._buf.read(1), self._order)

    def read_i16(self):
        return int.from_bytes(self._buf.read(2), self._order)

    def read_i32(self):
        return int.from_bytes(self._buf.read(4), self._order)

    def read_i64(self):
        return int.from_bytes(self._buf.read(8), self._order)

    def read_f32(self):
        return struct.unpack('<f', self._buf.read(4))

    def read_f64(self):
        return struct.unpack('<d', self._buf.read(8))

    def read_sized_ascii_string(self):
        size = self.read_i32()
        return self._buf.read(size).decode('ascii').strip('\00')

    def skip(self, n: int):
        self._buf.read(n)

    def close(self):
        self._buf.close()


class Flight:
    def __init__(self, buf: Buf):
        buf.skip(24)

        self.player_start_time = datetime.datetime.utcfromtimestamp(buf.read_i32())

        buf.skip(4)  # Unknown - appears to be constant 0

        self.flight_type = buf.read_sized_ascii_string()
        self.flight_start_time = (buf.read_i16(), buf.read_i16(), buf.read_i16(), buf.read_i16(), buf.read_i16())

        buf.skip(10)

        self.flight_departure_place = buf.read_sized_ascii_string()
        self.flight_arrival_place = buf.read_sized_ascii_string()

        buf.skip(38)

        self.plane_model_source = buf.read_sized_ascii_string()

        buf.skip(8)

        self.plane_model_type = buf.read_sized_ascii_string()
        self.plane_model_id = buf.read_sized_ascii_string()
        self.plane_model_name = buf.read_sized_ascii_string()

        buf.skip(26)

        self.weather = buf.read_sized_ascii_string()

        buf.skip(2962)  # TODO: Temporary

    def __repr__(self) -> str:
        return f"Flight{{ " \
               f"flight_type={self.flight_type} " \
               f"player_start_time={self.player_start_time} " \
               f"flight_start_time={self.flight_start_time} " \
               f"departure_place={self.flight_departure_place} " \
               f"arrival_place={self.flight_arrival_place} " \
               f"plane_model_source={self.plane_model_source} " \
               f"plane_model_type={self.plane_model_type} " \
               f"plane_model_id={self.plane_model_id} " \
               f"plane_model_name={self.plane_model_name} " \
               f"weather={self.weather} " \
               f"}}"


class Logbook:
    _MAGIC_COMPATIBLE_VERSION = (8,)

    def __init__(self, buf: Buf):
        self.version = buf.read_i32()
        self.total_flights = buf.read_i32()  # TODO: Check if -1

        # self.flights = [Flight(buf) for _ in range(self.total_flights)]
        self.flights = [Flight(buf), Flight(buf)]  # TODO: Only reading the first 2 flights for now


def parse(file: str):
    with open(file, mode='rb') as f:
        buf = Buf(BytesIO(f.read()))

    logbook = Logbook(buf)
    print(repr(logbook.flights))
    print("----")
    print("Logbook version:", logbook.version)
    print("Total flights:", logbook.total_flights)


if __name__ == '__main__':
    parse(sys.argv[1])
