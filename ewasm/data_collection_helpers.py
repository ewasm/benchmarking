

def get_runtimes_from_stderr_textfile(infile,engine,testcase,outfile):
  # this function reads file with runtime data and collects runtimes into runtimes.txt
  fin = open(infile, 'r')
  fout = open(outfile, 'a')
  instantiation_times = []
  invocation_times = []
  for line in fin:
    #looking for lines of form:   Time [us]: 301874 = 301056 + 817
    if line[0:10] == "Time [us]:":
      words = line.split() #split on whitespace
      instantiation_times.append(int(words[4]))
      invocation_times.append(int(words[6]))
  # if there are multiple times for a given test, then the last times can be dropped because they are for the contract which calls the contract to be benchmarked
  if len(invocation_times)>1:
    instantiation_times = instantiation_times[:-1]
    invocation_times = invocation_times[:-1]
  instantiation_time_str = engine+" "+testcase+" instantiation_time " + ','.join([str(e) for e in instantiation_times])
  invocation_time_str    = engine+" "+testcase+" invocation_time " +   ','.join([str(e) for e in invocation_times])
  fout.write("\n\n"+instantiation_time_str)
  fout.write("\n"  +invocation_time_str)
  print(instantiation_time_str)
  print(invocation_time_str)
  fin.close()
  fout.close()


if __name__ == "__main__":
  import sys
  if len(sys.argv)!=5:
    print("should be: pyton3( <infile> , <engine> , <testcase> , <outfile> )")
    print("read the source code, it is short")
  else:
    get_runtimes_from_stderr_textfile(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])


