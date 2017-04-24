import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

#LogisticClassification 다중 변수 또는 단일변수 둘다 사용 가능
#입력값은 x[i]가 통채로 하나씩 들어간다.
#x_data의 shape는  (데이터의 수  , feature의 수)또는 1차원인경우 (입력데이터집합의 개수)
#y_data의 shape는 1차원이 나오고 (예측데이터 집합의 개수 =입력데이터 집합의 개수)
#y_data학습할 때는 반드시 0또는 1이여야 한다.
class LogisticClassification2:

    x_data = None
    y_data = None
    W_val = []
    cost_val = []
    X_val = []
    Y_val = []
    list_step = []
    X = None
    Y = None
    weights = []
    bias = []
    hypothesis = None
    cost = None
    learning_rate=None
    sess= None
    layer = 0
    dic = []

    def __init__(self,x_data,y_data,dic):
        self.one_D = True
        self.x_data = x_data
        self.y_data = y_data
        self.sess = tf.Session()
        #rank=1인지 2인지 판단

        x = x_data[0][0]
        self.X = tf.placeholder(tf.float32,[None, None])
        self.Y = tf.placeholder(tf.float32, [None, None])

        self.dic = dic
        self.w1 = tf.Variable(tf.random_uniform([len(dic[0])]))
        self.w2 = tf.Variable(tf.random_uniform([len(dic[1])]))
        self.w3 = tf.Variable(tf.random_uniform([len(dic[2])]))
        self.w4 = tf.Variable(tf.random_uniform([len(dic[3])]))
        self.w5 = tf.Variable(tf.random_uniform([len(dic[4])]))
        # self.w6 = tf.Variable(tf.random_uniform([len(dic[5])]))
        # self.w7 = tf.Variable(tf.random_uniform([len(dic[6])]))
        # self.w8 = tf.Variable(tf.random_uniform([len(dic[7])]))

        for i in range(len(x_data)):
            for j in range(len(x_data[0])):
                x = dic[j].index(x_data[i][j])
                if j == 0:
                    self.x_data[i][j] = self.w1[x]
                elif j == 1:
                    self.x_data[i][j] = self.w2[x]
                elif j == 2:
                    self.x_data[i][j] = self.w3[x]
                elif j == 3:
                    self.x_data[i][j] = self.w4[x]
                elif j == 4:
                    self.x_data[i][j] = self.w5[x]
                # elif j == 5:
                #     self.x_data[i][j] = self.w6[x]
                # elif j == 6:
                #     self.x_data[i][j] = self.w7[x]
                # elif j == 7:
                #     self.x_data[i][j] = self.w8[x]

    def create_layer(self, X, input_length, output_length):
        self.weights.append(tf.Variable(tf.random_uniform([input_length, output_length],-1.0,1.0)))
        self.bias.append(tf.Variable(tf.random_uniform([output_length], -1.0, 1.0)))

        ret = tf.add(tf.matmul(X, self.weights[-1]),self.bias[-1])
        self.layer += 1
        ret = tf.nn.relu(ret)
        return ret


    def set_cost(self, input_data, input_length):
        self.bias.append(tf.Variable(tf.random_uniform([len(self.y_data[0])], -1.0, 1.0)))
        self.weights.append(tf.Variable(tf.random_uniform([input_length, len(self.y_data[0])], -1.0, 1.0)))
        self.hypothesis = tf.div(1., 1. + tf.exp(tf.matmul(input_data, -self.weights[-1] ) + self.bias[-1]))
        self.cost = -tf.reduce_mean(self.Y * tf.log(self.hypothesis) + (1 - self.Y) * tf.log(1 - self.hypothesis))

        init = tf.initialize_all_variables()
        self.sess.run(init)


    def training(self, learning_rate=0.04, step=2001, show_training_data=False):
        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate)
        self.train = self.optimizer.minimize(self.cost)
        self.list_step = range(step)
        for step in range(step):
            self.sess.run(self.train, feed_dict={self.X: self.sess.run(self.x_data), self.Y: self.y_data})
            self.cost_val.append(
                self.sess.run(self.cost, feed_dict={self.X: self.sess.run(self.x_data), self.Y: self.y_data}))
            if show_training_data == True and step % 20 == 0:
                print(step, 'weght = ',
                      self.sess.run(self.weights[-1],
                                    feed_dict={self.X: self.sess.run(self.x_data), self.Y: self.y_data}),
                      'cost =',
                      self.sess.run(self.cost, feed_dict={self.X: self.sess.run(self.x_data), self.Y: self.y_data}))
        plt.plot(self.list_step, self.cost_val)
        plt.ylabel('cost')
        plt.xlabel('step')

    def show_cost_graph(self):
        plt.plot(self.list_step, self.cost_val)
        plt.ylabel('cost')
        plt.xlabel('step')
        plt.show()
    # 입력값이 1차원이였을 때 입력값과 라벨을 보여준다.
    # def show_singlevariable_graph(self):
    #     try:
    #         plt.plot(self.x_data, self.y_data, 'ro')
    #         plt.plot(self.x_data, self.sess.run(tf.div(1.,1.+tf.exp(-self.W  * (self.x_data-self.b)))), label='fitted line')
    #         plt.ylabel('hypothesis')
    #         plt.xlabel('X')
    #         plt.legend()
    #         plt.show()
    #     except:
    #         print('입력값이 1차원이 아닙니다.')

    # 입력값을 형식에 맞게 넣은 경우 회귀에 따른 예측값을 보여준다.
    def predict(self, x_data):
        for i in range(len(x_data)):
            for j in range(len(x_data[0])):
                if j == 0:
                    if x_data[i][j] >= self.dic[j][len(self.dic[j])-1]:
                        x = self.dic[j].index(self.dic[j][len(self.dic[j])-1])
                        x_data[i][j] = self.w1[x] + (self.w1[x]-self.w1[x-1]) * (x_data[i][j] - self.dic[j][len(self.dic[j])-1])/(self.dic[j][len(self.dic[j])-1] - self.dic[j][len(self.dic[j])-2])
                    else:
                        for k in range(len(self.dic[j]) - 1):
                            if self.dic[j][k] <= x_data[i][j] < self.dic[j][k+1]:
                                x = self.dic[j].index(self.dic[j][k])
                                x_data[i][j] = self.w1[x] + (self.w1[x+1]-self.w1[x])*(x_data[i][j] - self.dic[j][k])/(self.dic[j][k +1] - self.dic[j][k])
                                break;
                elif j == 1:
                    if x_data[i][j] >= self.dic[j][len(self.dic[j])-1]:
                        x = self.dic[j].index(self.dic[j][len(self.dic[j])-1])
                        x_data[i][j] = self.w2[x] + (self.w2[x]-self.w2[x-1]) * (x_data[i][j] - self.dic[j][len(self.dic[j])-1])/(self.dic[j][len(self.dic[j])-1] - self.dic[j][len(self.dic[j])-2])
                    else:
                        for k in range(len(self.dic[j])):
                            if self.dic[j][k] <= x_data[i][j] < self.dic[j][k+1]:
                                x = self.dic[j].index(self.dic[j][k])
                                x_data[i][j] = self.w2[x] + (self.w2[x+1]-self.w2[x])*(x_data[i][j] - self.dic[j][k])/(self.dic[j][k +1] - self.dic[j][k])
                                break;
                elif j == 2:
                    if x_data[i][j] >= self.dic[j][len(self.dic[j])-1]:
                        x = self.dic[j].index(self.dic[j][len(self.dic[j])-1])
                        x_data[i][j] = self.w3[x] + (self.w3[x]-self.w3[x-1]) * (x_data[i][j] - self.dic[j][len(self.dic[j])-1])/(self.dic[j][len(self.dic[j])-1] - self.dic[j][len(self.dic[j])-2])
                    else :
                        for k in range(len(self.dic[j])):
                            if self.dic[j][k] <= x_data[i][j] < self.dic[j][k+1]:
                                x = self.dic[j].index(self.dic[j][k])
                                x_data[i][j] = self.w3[x] + (self.w3[x+1]-self.w3[x])*(x_data[i][j] - self.dic[j][k])/(self.dic[j][k +1] - self.dic[j][k])
                                break;
                elif j == 3:
                    if x_data[i][j] >= self.dic[j][len(self.dic[j])-1]:
                        x = self.dic[j].index(self.dic[j][len(self.dic[j])-1])
                        x_data[i][j] = self.w4[x] + (self.w4[x]-self.w4[x-1]) * (x_data[i][j] - self.dic[j][len(self.dic[j])-1])/(self.dic[j][len(self.dic[j])-1] - self.dic[j][len(self.dic[j])-2])
                    else :
                        for k in range(len(self.dic[j])):
                            if self.dic[j][k] <= x_data[i][j] < self.dic[j][k+1]:
                                x = self.dic[j].index(self.dic[j][k])
                                x_data[i][j] = self.w4[x] + (self.w4[x+1]-self.w4[x])*(x_data[i][j] - self.dic[j][k])/(self.dic[j][k +1] - self.dic[j][k])
                                break;
                elif j == 4:
                    if x_data[i][j] >= self.dic[j][len(self.dic[j])-1]:
                        x = self.dic[j].index(self.dic[j][len(self.dic[j])-1])
                        x_data[i][j] = self.w5[x] + (self.w5[x]-self.w5[x-1]) * (x_data[i][j] - self.dic[j][len(self.dic[j])-1])/(self.dic[j][len(self.dic[j])-1] - self.dic[j][len(self.dic[j])-2])
                    else :
                        for k in range(len(self.dic[j])):
                            if self.dic[j][k] <= x_data[i][j] < self.dic[j][k+1]:
                                x = self.dic[j].index(self.dic[j][k])
                                x_data[i][j] = self.w5[x] + (self.w5[x+1]-self.w5[x])*(x_data[i][j] - self.dic[j][k])/(self.dic[j][k +1] - self.dic[j][k])
                                break;
                elif j == 5:
                    if x_data[i][j] >= self.dic[j][len(self.dic[j])-1]:
                        x = self.dic[j].index(self.dic[j][len(self.dic[j])-1])
                        x_data[i][j] = self.w6[x] + (self.w6[x]-self.w6[x-1]) * (x_data[i][j] - self.dic[j][len(self.dic[j])-1])/(self.dic[j][len(self.dic[j])-1] - self.dic[j][len(self.dic[j])-2])
                    else :
                        for k in range(len(self.dic[j])):
                            if self.dic[j][k] <= x_data[i][j] < self.dic[j][k+1]:
                                x = self.dic[j].index(self.dic[j][k])
                                x_data[i][j] = self.w6[x] + (self.w6[x+1]-self.w6[x])*(x_data[i][j] - self.dic[j][k])/(self.dic[j][k +1] - self.dic[j][k])
                                break;
                # elif j == 6:
                #     if x_data[i][j] >= self.dic[j][len(self.dic[j])-1]:
                #         x = self.dic[j].index(self.dic[j][len(self.dic[j])-1])
                #         x_data[i][j] = self.w7[x] + (self.w7[x]-self.w7[x-1]) * (x_data[i][j] - self.dic[j][len(self.dic[j])-1])/(self.dic[j][len(self.dic[j])-1] - self.dic[j][len(self.dic[j])-2])
                #     else :
                #         for k in range(len(self.dic[j])):
                #             if self.dic[j][k] <= x_data[i][j] < self.dic[j][k+1]:
                #                 x = self.dic[j].index(self.dic[j][k])
                #                 x_data[i][j] = self.w7[x] + (self.w7[x+1]-self.w7[x])*(x_data[i][j] - self.dic[j][k])/(self.dic[j][k +1] - self.dic[j][k])
                #                 break;
                # elif j == 7:
                #     if x_data[i][j] >= self.dic[j][len(self.dic[j])-1]:
                #         x = self.dic[j].index(self.dic[j][len(self.dic[j])-1])
                #         x_data[i][j] = self.w8[x] + (self.w8[x]-self.w8[x-1]) * (x_data[i][j] - self.dic[j][len(self.dic[j])-1])/(self.dic[j][len(self.dic[j])-1] - self.dic[j][len(self.dic[j])-2])
                #     else :
                #         for k in range(len(self.dic[j])):
                #             if self.dic[j][k] <= x_data[i][j] < self.dic[j][k+1]:
                #                 x = self.dic[j].index(self.dic[j][k])
                #                 x_data[i][j] = self.w8[x] + (self.w8[x+1]-self.w8[x])*(x_data[i][j] - self.dic[j][k])/(self.dic[j][k +1] - self.dic[j][k])
                #                 break;
        temp = x_data
        for i in range(len(self.weights) - 1):
            temp = tf.matmul(temp, self.weights[i])
        self.hypothesis = tf.div(1., 1. + tf.exp(tf.matmul(self.X, -self.weights[-1]) + self.bias[-1]))
        try:
            self.result = self.sess.run(self.hypothesis, feed_dict={self.X: self.sess.run(x_data)})
        except:
            self.result = self.sess.run(self.hypothesis, feed_dict={self.X: x_data})
        print (x_data)
        print (self.weights[-1])
        print(self.result)
        # self.Y_val = self.sess.run(self.hypothesis, feed_dict={self.X: self.sess.run(temp), self.Y: self.y_data})
        # self.X_val = x_data
        # print(self.result)
        # try:
        #     plt.plot(self.X_val, self.Y_val, 'ro')
        #     plt.plot(self.x_data,self.sess.run(tf.div(1.,1.+tf.exp(-self.W  * (self.x_data-self.b)))), label='fitted line')
        #     plt.ylabel('hypothesis')
        #     plt.xlabel('X')
        #     plt.legend()
        #     plt.show()
        # except:
        #      print('입력값이 1차원이 아닙니다.')

    def save_weight(self):
        wval = [self.w1, self.w2, self.w3, self.w4, self.w5]
        print(self.sess.run(wval))
        np.save('lvari', self.sess.run(wval))
        np.save('lweight', self.sess.run(self.weights))
        np.save('lbias', self.sess.run(self.bias))

    def load_weight(self):
        self.weights = np.load('lweight.npy')
        self.bias = np.load('lbias.npy')
        lvari = np.load('lvari.npy')
        self.w1 = lvari[0]
        self.w2 = lvari[1]
        self.w3 = lvari[2]
        self.w4 = lvari[3]
        self.w5 = lvari[4]
        # self.w6 = lvari[5]
        # self.w7 = lvari[6]
        # self.w8 = lvari[7]

    # 딥하게 갈수 있는 여지는 만들었지만 의미는 없는듯
    def create_layer(self, X, input_length, output_length):
        self.weights.append(tf.Variable(tf.random_uniform([input_length, output_length], -1.0, 1.0)))
        self.bias.append(tf.Variable(tf.random_uniform([output_length], -1.0, 1.0)))
        ret = tf.add(tf.matmul(X, self.weights[-1]), self.bias[-1])
        self.layer += 1
        ret = tf.nn.relu(ret)
        return ret