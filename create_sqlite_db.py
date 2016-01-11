import sqlite3
import features
import sys
import classification_starter
import util
import numpy as np

def create_table(conn, c, global_feat_dict):
    feat_names = ['"' + k + '"' for k in sorted(global_feat_dict.keys())]
    c.execute("DROP TABLE IF EXISTS data")
    c.execute('CREATE TABLE data (id,class,class_name,{0})'.format( ','.join(feat_names)))
    conn.commit()
    return

def write_data(conn, c, X_train, global_feat_dict, t_train, train_ids):
    batch = []
    feats = [k for k in sorted(global_feat_dict.keys())]
    # Question marks for SQL query (add 3 for id, class and class name)
    qmarks = ','.join(["?" for _ in xrange(len(feats) + 3)])

    # Write each datapoint to the batch
    for i in xrange(X_train.shape[0]):
        # Initialize this row with the datapoint's ID and class
        row = [train_ids[i], int(t_train[i]), util.malware_classes[t_train[i]]]
        for feat in feats:
            this_feat = convert_np_datatype(X_train[i,global_feat_dict[feat]])
            row.append(this_feat)
        batch.append(tuple(row))

        # Write entire batch every 100 data points
        if i % 100 == 99:
            c.executemany('INSERT INTO data VALUES({0})'.format(qmarks), batch)
            batch = []
            print "written ",i,"/", X_train.shape[0]
    # Write the last data points
    if batch:
        c.executemany('INSERT INTO data VALUES({0})'.format(qmarks), batch)
    print "write complete."

    conn.commit()

DATATYPE_CONVERSIONS = [('int32', int),
                        ('int64', int),
                        ('float32', float),
                        ('float64', float)]

def convert_np_datatype(elem):
    for orig_type, new_type in DATATYPE_CONVERSIONS:
        if type(elem).__name__ == orig_type:
            elem = new_type(elem)
            break
    return elem

def create_index(conn, c):
    c.execute("DROP INDEX IF EXISTS class_idx")
    c.execute("CREATE INDEX class_idx ON data (class)")
    c.execute("CREATE INDEX class_name_idx ON data (class_name)")
    conn.commit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "USAGE: create_sqlite_db.py [db_name] [num_data_points]"
        quit()
    if len(sys.argv) == 3:
        classification_starter.TOTAL_NUM_DATA = int(sys.argv[2])
        print "Using at most",classification_starter.TOTAL_NUM_DATA,"data points..."
    dbname = sys.argv[1]
    if dbname[-3:] != ".db":
        dbname = dbname + ".db"

    print "creating database..."
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # extract features
    ffs = features.ALL_FEATURES
    print "extracting training features..."
    train_dir = "train"
    X_train,global_feat_dict,t_train,train_ids = classification_starter.extract_feats(ffs, train_dir)

    print "creating table..."
    create_table(conn, c, global_feat_dict)
    print "writing data..."
    write_data(conn, c, X_train, global_feat_dict, t_train, train_ids)
    print "creating index..."
    create_index(conn, c)
    print "done!"




