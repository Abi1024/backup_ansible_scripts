from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark import StorageLevel
from pyspark import SparkConf
from graphframes import *
import time

def process_kron_input(filename):
    file = open (filename, 'r')
    vertex_file = open('/mnt/hadoop/vertices.csv','w')
    edges_file = open('/mnt/hadoop/edges.csv','w')
    first_line = True
    vertex_file.write("id\n")
    edges_file.write("src,dst\n")
    while True:
        line = file.readline()
        if not line:
            break
        line_array = line.strip().split()
        if first_line:
            num_nodes = int(line_array[0])
            num_edges = line_array[1]
            first_line = False
        else:
            edges_file.write(line_array[0] + "," + line_array[1] + "\n")
    for i in range(num_nodes):
        vertex_file.write(str(i)+"\n")
    file.close()
    vertex_file.close()
    edges_file.close()

#process_kron_input('/mnt/new_streams/kron_16_graph')
print("Done processing input into GraphX format")
sc = SparkContext("local","first app")
#sc = SparkContext("spark://slurm-head.cloud.compas.cs.stonybrook.edu:7077","first app")
#config = SparkConf().setAll([('spark.master',"spark://slurm-head.cloud.compas.cs.stonybrook.edu:7077"),('spark.app.name',"second app"),('spark.executor.memory', '6g'), ('spark.executor.cores', '4'), ('spark.driver.memory','6g'),('spark.network.timeout','300s')])
sc = SparkContext(conf=config)
sqlContext = SQLContext(sc)
#takes as input a pathname to a kronecker graph and generates a GraphX graph
sc.setLogLevel("WARN")

v = sqlContext.read.csv('/mnt/cloud/vertices.csv', header=True).persist(StorageLevel.MEMORY_AND_DISK)
e = sqlContext.read.csv('/mnt/cloud/edges.csv', header=True).persist(StorageLevel.MEMORY_AND_DISK)
g = GraphFrame(v, e).persist(StorageLevel.MEMORY_AND_DISK)
start_time = time.time()
result = g.connectedComponents(algorithm='graphx')
print("--- %s seconds ---" % (time.time() - start_time))
result.show()
print("Number of components: " + str(result.select("component").rdd.distinct().count()))
