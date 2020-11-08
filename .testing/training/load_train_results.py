import preprocessing.get_data as gd


data = gd.load_data('../../train_output.p')
print(len(data[2]))