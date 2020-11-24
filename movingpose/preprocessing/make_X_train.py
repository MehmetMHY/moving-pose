# generate the X_t matrix in form of
# [[P(t0), δP(t0), δP(t0), t0],
#  [P(t1), δP(t1), δP(t1), t1]]

# where
# P(t0) = [[x_1, y_1, z_1], ... ,[x_20, y_20, z_20]] for every joint
# δP(t0) = [ δP(t0)_1, ..., δP(t0)_20] for every joint

# load normalized skeleton data
import movingpose.preprocessing.get_data as gd
import movingpose.preprocessing.derivatives as d
import numpy as np

norm_train = gd.load_data('../pickle/norm_train.p')
X_train = {}

for data_set in norm_train:
    p_t = np.array(norm_train[data_set])[:, :, 2:]  # cut out the frame num and joint num
    print(p_t.shape)
    first_derivative = d.first_derivative(p_t)
    second_derivative = d.second_derivative(p_t)
    t = np.arange(1, len(norm_train[data_set]) + 1)
    X_train_t = [p_t, first_derivative, second_derivative, t]
    X_train[data_set] = X_train_t
    print(f'Created X_train for {data_set}')
    break
#gd.save_data('../pickle/X_train.p', X_train)




