import sys
sys.path.append(".")

def str2float(item):
    if 'e' not in item:
        return float(item)
    itemVec = item.split('e')
    num = float(itemVec[0])
    exp = 1
    if itemVec[1][0] == '+':
        exp = 10 ** int(itemVec[1][1:])
    else:
        exp = 0.1 ** int(itemVec[1][1:])

    return num * exp


if __name__ == "__main__": 
    fileList = ["./static/basechannel114_res.csv","./static/andlutchannel114_res.csv","./static/andanddlutRvpr114_res.csv", "./static/base_res_lut7_114.csv"]
    # fileList = ["./basechannel114_res.csv","./andlutchannel114_res.csv","./andandlutchannel114_res.csv"]
    results = []

    line = "LU32PEEng.odin.blif  arm_core.odin.blif  blob_merge.odin.blif  mcml.odin.blif              mkPktMerge.odin.blif     or1200.odin.blif     sha.odin.blif    stereovision0.odin.blif  stereovision2.odin.blif \
            LU8PEEng.odin.blif   bgm.odin.blif       boundtop.odin.blif    mkDelayWorker32B.odin.blif  mkSMAdapter4B.odin.blif  raygentop.odin.blif  spree.odin.blif  stereovision1.odin.blif  stereovision3.odin.blif"
    lineVec = line.split()
    carelist = []
    for file in lineVec:
        carelist.append(file[:-10])

    params = []
    with open(fileList[0], 'r') as fi:
        bench = {}
        line = fi.readline()
        lineVec = line.replace('\n','').replace(' ','').split(",")
        for item in lineVec[1:]:
            params.append(item)
        while line:
            line = fi.readline()
            if len(line) == 0:
                continue
            lineVec = line.replace('\n','').replace(' ','').split(",")
            if len(carelist) > 0 and lineVec[0][:-5] not in carelist:
                continue
            bench[lineVec[0][:-5]]=[]
            for item in lineVec[1:]:
                bench[lineVec[0][:-5]].append(str2float(item))
        results.append(bench)
    

    for file in fileList[1:]:
        with open(file, 'r') as fi:
            bench = {}
            line = fi.readline()
            while line:
                line = fi.readline()
                if len(line) == 0:
                    continue
                lineVec = line.replace('\n','').replace(' ','').split(",")
                if len(carelist) > 0 and lineVec[0] not in carelist:
                    continue
                bench[lineVec[0]]=[]
                for item in lineVec[1:]:
                    bench[lineVec[0]].append(str2float(item))
        results.append(bench)

    data = []

    for idx in range(1, len(results)):
        benchdata = {}
        parsum = [0.0] * len(params)
        parnum = [0] * len(params)
        for bench in results[idx]:
            if len(results[idx][bench]) != len(params):
                continue
            benchdata[bench] = []
            for idy in range(0, len(params)):
                if results[idx][bench][idy] == 0 or results[0][bench][idy] == 0:
                    benchdata[bench].append(-2.0)
                else:
                    deviation = results[idx][bench][idy] / results[0][bench][idy] - 1
                    benchdata[bench].append(deviation)
                    parnum[idy]+=1
                    parsum[idy]+=deviation
            benchdata["__avg__"] = []
            for idy in range(0, len(params)):
                if parnum[idy] == 0:
                    benchdata["__avg__"].append(-2.0)
                else:
                    benchdata["__avg__"].append(parsum[idy]/parnum[idy])
        data.append(benchdata)

    for param in params:
        print(param,end=" ")
    print()
    for idx in range(0, len(data)):
        print("=============  "+fileList[1+idx]+"  ============")
        for bench in data[idx]:
            print(bench,end=" : ")
            print(' ' * (30 - len(bench)),end="")
            for idy in range(0, len(params)):
                if(data[idx][bench][idy] == -2.0):
                    print("null",end=", ")
                else:
                    print(round(data[idx][bench][idy] * 100, 1),end=", ")
            print()
        print()
    