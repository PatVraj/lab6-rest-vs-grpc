RPC values are average time per operation; PING values are average roundtrip time.

| Method          | Local  | Same-Zone | Different Region |
|-----------------|-------:|----------:|-----------------:|
| REST add        | 2.980  | 4.381     | 481.286          |
| gRPC add        | 0.892  | 1.513     | 180.511          |
| REST rawimg     | 5.860  | 10.008    | 1884.307         |
| gRPC rawimg     | 7.817  | 10.577    | 176.480          |
| REST dotproduct | 3.737  | 4.924     | 401.862          |
| gRPC dotproduct | 0.864  | 1.444     | 162.186          |
| REST jsonimg    | 41.131 | 46.156    | 2188.269         |
| gRPC jsonimg    | 18.758 | 20.517    | 360.812          |
| PING            | 0.048  | 0.565     | 160.885          |

Local and same zone RPC tests used 1,000 repetitions each. Different region RPC tests used 100 repetitions each. Each ping test used 10 packets.

gRPC was faster for most operations, with the largest differences appearing across regions. Network latency increased from 0.565 ms within the same zone to 160.885 ms across regions. The REST client establishes a new TCP connection for each query, adding connection setup and extra network round trips, while gRPC reuses one TCP connection across queries. This helps explain why cross region REST add took 481.286 ms compared with 180.511 ms for gRPC. Ping provides a network baseline without RPC processing or Python overhead, although RPC timing also includes data transfer, serialization, and application work. gRPC was not always faster, the REST rawimg calls were slightly faster locally and within the same zone.
