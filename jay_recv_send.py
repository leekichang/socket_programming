def send_recv_data(weights):
    global CUR_ROUND
    
    local_weight_list_1, local_weight_list_2, key_list = extract_weights(weights)
    HOST = '1.233.219.178'
    PORT = 9000

    conn_flag = False
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.connect((HOST, PORT))
    
    while not conn_flag:
        try:
            client_socket.connect((HOST, PORT))
            conn_flag = True
            client_socket.settimeout(None)
        except socket.error:
            time.sleep(10)
    '''
    STEP 0. Send user ID
    '''
    client_socket.sendall(str(USER_ID).encode())
    time.sleep(1)
    
    '''
    STEP 1. Receive the current global round#
    '''
    CUR_ROUND  = int(client_socket.recv(1024).decode())
    time.sleep(1)
    print('Current Global Round: ', CUR_ROUND)

    '''
    STEP 2. Send local weights
    '''
    data = pickle.dumps(local_weight_list_1)
    print(np.shape(data), ', ', len(data))
    client_socket.sendall(str(len(data)).encode())

    time.sleep(1)
    client_socket.sendall(data)

    time.sleep(2)
    data = pickle.dumps(local_weight_list_2)
    print(np.shape(data), ', ', len(data))
    client_socket.sendall(str(len(data)).encode())

    time.sleep(1)
    client_socket.sendall(data)

    time.sleep(2)

    '''
    STEP 3. Receive updated global weights
    '''
    data_total_len     = int(client_socket.recv(1024))
    left_receiving_len = data_total_len
    print('The length of receiving data: ', data_total_len)
    buffer_size        = data_total_len

    total_data = b''
    while(True):

        received_data = client_socket.recv(buffer_size)
        total_data   += received_data

        left_receiving_len = left_receiving_len - len(received_data)
        #print('---- Received data len: ', len(received_data), ', left: ', left_receiving_len)

        if left_receiving_len <= 0:
            print('---- Finished!')
            break

    client_socket.close()
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    return pickle.loads(total_data), key_list