# Προετοιμασία
* παίρνουμε το csv αρχείο από το φοιτητολόγιο ``<inputcsvfile>``
* Δημιουργούμε μια νέα στήλη όπου θα βάλουμε το path για τα αρχεία που δημιουργήσαμε ώστε να σταλούν στους φοιτητές
* εντοπίζουμε τις στήλες με το email και το attachment και το θέτουμε σαν παραμέτρους στο αρχείο mailsubjects.conf
* Δημιουργία google form για την υποβολή τψν απαντήσεων


Παραμετροποίηση του email body.txt με το όνομα μαθήματος, τις ώρες εξέτασης και το google form link που θα υποβληθούν.

```bash
sed 's/--COURSE--/Κατανεμημενα Συστηματα/g; s/--TIME-LIMIT--/δυο (2)/g; s#--FORM-LINK--#https://form.link#g' body.txt > custom_body.txt  
```
# Εκτέλεση

```bash
python mailsubjects.py -i <inputcsvfile> -l <logfile> \ 
-e <emailbodyfile> -u <sender mail address>, -p <password> \
-s <subject mail>
```
Παράδειγμα:
```bash
python mailsubjects.py -i sample.csv -l sample.log -e custom_body.txt -u tsadimas@staff.hua.gr -p 'password' -s "θΕΜΑΤΑ ΕΞΕΤΑΣΕΩΝ ΣΤΑ ΚΑΤΑΝΕΜΗΜΕΝΑ ΣΥΣΤΗΜΑΤΑ"
```
Εναλλακτικά
```bash
python mailsubjects.py -c mailsubjects.conf
```
