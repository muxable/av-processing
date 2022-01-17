import av
import sys

def main():
    source = av.open("pipe:", format="avi", mode="r")
    source_v = source.streams.video[0]
    source_a = source.streams.audio[0]

    sink = av.open("pipe:", format="avi", mode="w")
    sink_v = sink.add_stream(template=source_v)
    sink_a = sink.add_stream(template=source_a)

    for packet in source.demux():
        if packet is None:
            continue
        for frame in packet.decode():
            index = frame.index
            if packet.stream.type == 'video':
                packet.stream = sink_v
            else:
                packet.stream = sink_a

            sink.mux(packet)
    sink.close()

if __name__ == '__main__':
    main()