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

process_kron_input('/mnt/hadoop/kron_13_unique_half.txt')

