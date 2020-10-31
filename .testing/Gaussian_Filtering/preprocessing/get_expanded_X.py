import preprocessing.get_data as gd


# def get_all_data():
#     """
#     :return: matrix X with every frame from every action in form of [descriptor, t, label]
#     """
#     all_data = gd.load_data('pickle/train.p')
#     X = []
#
#     for label in all_data.keys():
#         for *descriptor, t in all_data[label]:
#             X.append([*descriptor, ])
a = [1,2,3]
b = [*a, 't', 'b']

print(b)