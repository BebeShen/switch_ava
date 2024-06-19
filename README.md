# switch avaliability check

Check it every 4 hour

```shell
0 */4 * * * /usr/bin/python ~/Desktop/Projects/switch_check/switch_conn_test.py > ~/Desktop/imslab/switch_status/conn.log
```