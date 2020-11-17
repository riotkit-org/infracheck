import os
import inspect
import unittest
import influxdb
from tests.utils.influxdb_test import InfluxDBContainerRequirement, USER, PASSWORD, DB


# import a script with "-" in filename
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
with open(path + '/infracheck/checks/influxdb-query', 'r') as script:
    exec(script.read())


class InfluxDBQueryCheckTest(InfluxDBContainerRequirement, unittest.TestCase):
    def test_finds_occurrence_in_json_results(self):
        client = influxdb.InfluxDBClient(host='localhost', port=8086)
        client.switch_database(DB)
        client.switch_user(USER, PASSWORD)

        try:
            for i in range(1, 5):
                client.write_points([
                    {
                        "measurement": "cpu_load_short",
                        "tags": {
                            "host": "server01",
                            "region": "us-west"
                        },
                        "time": "2009-11-10T23:00:{}Z".format(i * 10),
                        "fields": {
                            "value": 0.64 + (i * 10)
                        }
                    }
                ])

            check = InfluxDBQueryCheck(
                host='localhost', port=8086,
                user=USER, password=PASSWORD,
                database=DB
            )

            result, message = check.main('select value from cpu_load_short;', '"value": 10.64')

            self.assertEqual('Query results are matching', message)
            self.assertTrue(result)
        finally:
            client.close()

    def test_will_not_find_occurrence(self):
        client = influxdb.InfluxDBClient(host='localhost', port=8086)
        client.switch_database(DB)
        client.switch_user(USER, PASSWORD)

        try:
            check = InfluxDBQueryCheck(
                host='localhost', port=8086,
                user=USER, password=PASSWORD,
                database=DB
            )

            result, message = check.main('select value from this_metrics_does_not_exist;', '"value": 10.64')

            self.assertEqual('Expected \'[]\' to contain \'"value": 10.64\'', message)
            self.assertFalse(result)
        finally:
            client.close()
