# ddps_2

This repository contains our implementation of our (toy) distributed data processing system. It implements the [Chord protocol](<https://en.wikipedia.org/wiki/Chord_(peer-to-peer)>).

It is implemented in Python and makes use of the [gRPC](https://grpc.io/) library for inter node communication.

This implementation also features replication across 2 nodes for all of your keys.

The state after an experiment is saved by the use of tags in the repository.
