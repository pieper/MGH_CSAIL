import csv
import re
import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.graph_objs import *

def ruleBasedCheck(current):
    # Check parameter-determined T1/T2/other
    t1Counter = 0
    t2Counter = 0
    if ((current[1] != '') and (current[2] != '') and
        (current[3] != '') and (current[4] != '')):
        try:
            float(current[1])
            if float(current[1]) < 1125: # Repetition Time (1125 divide, T1 being less)
                t1Counter += 1
            elif float(current[1]) < 20000:
                t2Counter += 1
        except ValueError:
            pass

        try:
            float(current[1])
            if float(current[1]) < 57.5: # Echo Time (57.5 divide, T1 being less)
                t1Counter += 1
            elif float(current[1]) < 250:
                t2Counter += 1
        except ValueError:
            pass

        try:
            float(current[2])
            if float(current[2]) < 8: # Echo Train Length (8 divide, T1 being less)
                t1Counter += 1
            else:
                t2Counter += 1
        except ValueError:
            pass

#t2: 90
#t1:0-30
        try:
            float(current[3])
            if (0 <= float(current[3])) and (float(current[3]) <= 30):
                t1Counter += 1
            elif float(current[3]) == 90: # Flip Angle (both checked as <=90 degrees)
                t2Counter += 1
        except ValueError:
            pass
    else:
        return 'incomplete'

    if t1Counter > t2Counter:
        return 't1'
    elif t2Counter > t1Counter:
        return 't2'
    else:
        return 'neither'

with open('/Users/jbt/Desktop/Lily/Sets_and_subsets/seriesDescrip_t1t2.csv', 'rU') as data_file:
    with open('/Users/jbt/Desktop/Lily/Sets_and_subsets/seriesDescrip_t1t2_predictions.csv', 'wb') as new_file:
    # Each list involves entire object
        t1PredictT2_TE = []
        t1PredictT2_TR = []
        t1PredictT2_lineNum = []

        t1PredictOther_TE = []
        t1PredictOther_TR = []
        t1PredictOther_lineNum = []

        t2PredictT1_TE = []
        t2PredictT1_TR = []
        t2PredictT1_lineNum = []

        t2PredictOther_TE = []
        t2PredictOther_TR = []
        t2PredictOther_lineNum = []

        incompleteCounter = 0
        incomplete_lineNum = []

        mismatchedCounter = 0
        rowCt = 0

        try:
            reader = csv.reader(data_file)
            writer = csv.writer(new_file, delimiter=',')
            for row in reader:
                if rowCt != 0:
                    predict = ruleBasedCheck(row)
                    row[7] = predict
                    if row[6] == row[7]:
                        pass
                    elif predict == 't2': # gets here if predict = 't2' and ground truth is 't1'
                        try:
                            float(row[1])
                            float(row[2])
                            t1PredictT2_TR.append(float(row[1]))
                            t1PredictT2_TE.append(float(row[2]))
                            t1PredictT2_lineNum.append(row[0])
                            mismatchedCounter +=1
                        except ValueError:
                            pass
                    elif predict == 't1': # gets here if predict = 't1' and ground truth is 't2'
                        try:
                            float(row[1])
                            float(row[2])
                            t2PredictT1_TR.append(float(row[1]))
                            t2PredictT1_TE.append(float(row[2]))
                            t2PredictT1_lineNum.append(row[0])
                            mismatchedCounter += 1
                        except ValueError:
                            pass
                    elif (predict == 'neither') and (row[6] == 't1'):
                        try:
                            float(row[1])
                            float(row[2])
                            t1PredictOther_TR.append(float(row[1]))
                            t1PredictOther_TE.append(float(row[2]))
                            t1PredictOther_lineNum.append(row[0])
                            mismatchedCounter += 1
                        except ValueError:
                            pass
                    elif (predict == 'neither') and (row[6] == 't2'):
                        try:
                            float(row[1])
                            float(row[2])
                            t2PredictOther_TR.append(float(row[1]))
                            t2PredictOther_TE.append(float(row[2]))
                            t2PredictOther_lineNum.append(row[0])
                            mismatchedCounter += 1
                        except ValueError:
                            pass
                    elif predict == 'incomplete':
                        incompleteCounter += 1
                        mismatchedCounter += 1
                        incomplete_lineNum.append(row[0])
                else:
                    rowCt += 1
                writer.writerow(row)
            print 'Including incomplete series, there are a total of %d mismatched series. Specifically, there are %d series with incomplete fields (TE/TR/ETL/FA) on original file lines:' % (mismatchedCounter, incompleteCounter)
            print(", ".join(incomplete_lineNum))

            '''
            plotly version. Used only for plotting, and you would need to login to the site in order to generate so please ignore this chunk for now

            trace0 = Scatter(x=t1PredictT2_TR, y=t1PredictOther_TE, mode='markers', name='T1W-Labeled, T2W-Predicted', text=t1PredictT2_lineNum, marker=Marker(size=12,))

            trace1 = Scatter(x=t1PredictOther_TR, y=t1PredictOther_TE, mode='markers', name='T1W-Labeled, Other-Predicted', text=t1PredictOther_lineNum, marker=Marker(size=12,))

            trace2 = Scatter(x=t2PredictT1_TR, y=t2PredictT1_TE, mode='markers', name='T2W-Labeled, T1W-Predicted', text=t2PredictT1_lineNum, marker=Marker(size=12,))

            trace3 = Scatter(x=t2PredictOther_TR, y=t2PredictOther_TE, mode='markers', name='T2W-Labeled, Other-Predicted', text=t2PredictOther_lineNum, marker=Marker(size=12,))

            dataToUse = Data([trace0, trace1, trace2, trace3])

            layout = Layout(xaxis=XAxis(autorange=True), yaxis=YAxis(autorange=True))

            fig = Figure(data=dataToUse, layout=layout)
            unique_url = py.plot(dataToUse, filename = 'Comparison of T1-T2 Subset')
            '''
            
            '''
            matplotlib version
            '''
            for color in ['red','blue','cyan', 'yellow']:
                if color == 'red':
                    plt.scatter(t1PredictT2_TR, t1PredictT2_TE, c=color, s=20, label='T1W-Labeled, T2W-Predicted', alpha=0.5, edgecolors='none')
                elif color == 'blue':
                    plt.scatter(t1PredictOther_TR, t1PredictOther_TE, c=color, s=20, label='T1W-Labeled, Other-Predicted', alpha=0.5, edgecolors='none')
                elif color == 'cyan':
                    plt.scatter(t2PredictT1_TR, t2PredictT1_TE, c=color, s=20, label='T2W-Labeled, T1W-Predicted', alpha=0.5, edgecolors='none')
                else:
                    plt.scatter(t2PredictOther_TR, t2PredictOther_TE, c=color, s=20, label='T2W-Labeled, Other-Predicted', alpha=0.5)
            plt.title('Echo Time vs. Repetition Time')
            plt.xlabel('Repetition Time (TR, msec)')
            plt.ylabel('Echo Time (TE, msec)')
            plt.legend()
            plt.grid(True)
            plt.show()
        finally:
            new_file.close()
    data_file.close()