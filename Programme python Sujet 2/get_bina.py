

def get_binary_data(image_path):
        with open(image_path, 'rb') as image_file:
            binary_data = image_file.read()
            image_file.close()
            #print(binary_data)
            
        return binary_data

