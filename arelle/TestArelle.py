import arelle
import time
from arelle import ViewFileFactList, ModelXbrl, ModelManager, FileSource, Cntlr, ModelDocument
import json
import os


def extractXbrl(path):
    # uses the black box that is arele (available on pip, it is a modified version done by Przemek and Rémi)
    modelManager = arelle.ModelManager.initialize(arelle.Cntlr.Cntlr())
    xbrl = arelle.ModelXbrl.load(modelManager, path)
    jsonobject = arelle.ViewFileFactList.viewFacts(xbrl, 'xbrlDocument.json')
    return jsonobject


def run_test(dir_with_samples):
    print("Running tests inside {}".format(dir_with_samples))
    for file in os.listdir(dir_with_samples):
        if not file.endswith('.xhtml'):
            continue
        path = os.path.join(dir_with_samples, file)

        # original code, without modifications
        ModelDocument.AWESOME_MODS = False
        st = time.time()
        org_raw = extractXbrl(path)
        org = json.dumps(org_raw)
        end = time.time()

        # turn on optimizations
        ModelDocument.AWESOME_MODS = True
        st2 = time.time()
        quick_raw = extractXbrl(path)
        quick = json.dumps(quick_raw)
        end2 = time.time()
        print("[{}] XBLR load: {:.3f}s vs. {:.3f}s".format(os.path.basename(path), end - st, end2 - st2))
        # if org != quick:
        #     print("Org: {}".format(org))
        #     print("Qck: {}\n".format(quick))

        filename = os.path.basename(path).split('.')[0]
        with open("out_{}_org.json".format(filename), 'wt') as f:
            json.dump(org_raw, f, indent=4)

        with open("out_{}_qck.json".format(filename), 'wt') as f:
            json.dump(quick_raw, f, indent=4)


if __name__ == "__main__":
    run_test('samples')
    exit(0)
    path = 'samples\\test01.xhtml'
    # original code, without modifications
    ModelDocument.AWESOME_MODS = False
    st = time.time()
    org = json.dumps(extractXbrl(path))
    end = time.time()

    # turn on optimizations
    ModelDocument.AWESOME_MODS = True
    st2 = time.time()
    quick = json.dumps(extractXbrl(path))
    end2 = time.time()
    print("[{}] XBLR load: {:.3f}s vs. {:.3f}s".format(os.path.basename(path), end - st, end2 - st2))
    if org != quick:
        print("Org: {}".format(org))
        print("Qck: {}\n".format(quick))
    print(org)
    print(quick)