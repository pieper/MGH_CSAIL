import csv
import re

def rowMod(lineNum, truth, txt, currentRow):
    currentRow.append(truth)
    currentRow.append(txt)
    currentRow.insert(0, lineNum)
    return currentRow

with open('/Users/jbt/Desktop/Lily/Sets_and_subsets/minimal-csv-baby-mr-tag.csv', 'rU') as data_file:
    with open('/Users/jbt/Desktop/Lily/Sets_and_subsets/seriesDescrip_t1t2.csv', 'wb') as new_file:

        try:
            reader = csv.reader(data_file)
            writer = csv.writer(new_file, delimiter=',')
            lineCounter = 0
            for row in reader:
                if (lineCounter != 0) and (row[4] != ''): # Sequence Name
                    seriesDescrip = row[4]
                    re.sub(r'\W+', '', seriesDescrip)
                    if re.search('t1', seriesDescrip, flags=re.IGNORECASE) and re.search('t2', seriesDescrip, flags=re.IGNORECASE):
                        pass
                    elif re.search('t1', seriesDescrip, flags=re.IGNORECASE):
                        writer.writerow(rowMod(lineCounter, 't1', 'TBD', row))
                    elif re.search('t2', seriesDescrip, flags=re.IGNORECASE):
                        writer.writerow(rowMod(lineCounter, 't2', 'TBD', row))
                elif (lineCounter == 0):
                    writer.writerow(('Row Number', 'TR', 'TE', 'ETL', 'FA', 'Series Description', 'Ground Truth', 'Predicted'))
                lineCounter += 1
        finally:
            new_file.close()
    data_file.close()