import statistics as stat
import matplotlib.pyplot as plt

def responses_umbral(responses, alpha):
    new_response = {}
    for key, list_datavalue in responses.items():
        new_response[key]= [datavalue.data for datavalue in responses[key] if datavalue.value > alpha]
    return new_response

def responses_r(responses, count):
    new_response = {}
    for key, list_datavalue in responses.items():
        new_response[key]= [datavalue.data for datavalue in responses[key]][:count]
    return new_response

def get_medidas(responses, qrels):
    medidas = {}
    for query_id, qrel in qrels.items():
        medidas[query_id] = (len(responses[query_id]), len(qrel), len(qrel.intersection(responses[query_id])))    
    return medidas

def get_recall_accuracy(medidas):
    recall = {}
    accuracy = {}
    for key, (rec, rel, rr) in medidas.items():
        if rec != 0:
            accuracy[key] = rr/rec
        else:        
            accuracy[key] = 0
        recall[key] = rr/rel
    return recall, accuracy

def plot_recall_accuracy(recall, accuracy):
    plt.scatter(recall.values(), accuracy.values(), alpha=0.1)
    recall_mean, accuracy_mean = stat.mean(recall.values()), stat.mean(accuracy.values())
    print(recall_mean, accuracy_mean)
    plt.scatter(recall_mean, accuracy_mean)

def plot_means(medidas, names):
    index = 0
    for recall, accuracy in medidas:
        recall_mean, accuracy_mean = stat.mean(recall.values()), stat.mean(accuracy.values())
        print(recall_mean, accuracy_mean)
        plt.scatter(recall_mean, accuracy_mean, label=names[index])
        index+=1
    plt.legend()
