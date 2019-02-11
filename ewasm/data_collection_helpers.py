

def get_runtimes_from_stderr_textfile(infile,engine,testcase,outfile):
  # this function reads stderr.txt and collects runtimes into runtimes.txt
  fin = open(infile, 'r')
  #fout_instantiation = open('runtimes_instantiation.txt', 'a')
  #fout_invocation = open('runtimes_invocation.txt', 'a')
  fout = open(outfile, 'a')
  instantiation_times = []
  invocation_times = []
  for line in fin:
    if line[0:15] == "Execution time:":
      words = line.split() #split on whitespace
      instantiation_times.append(int(words[5]))
      invocation_times.append(int(words[2])-int(words[5]))
      #fout_instantiation.write(", "+words[5])
      #fout_invocation.write(", "+str(int(words[2])-int(words[5])))
  # nested call runtimes are overwritten because of clumsy design in hera, and our generated scripts have nested calls
  # because of this, the last time can be dropped because they are inimportant
  if len(invocation_times)>1:
    instantiation_times = instantiation_times[:-1]
    invocation_times = invocation_times[:-1]
  fout.write("\n\n"+engine+" "+testcase+" instantiation_time " + ','.join([str(e) for e in instantiation_times]))
  fout.write("\n"  +engine+" "+testcase+" invocation_time " +   ','.join([str(e) for e in invocation_times]))
  print(engine+" "+testcase+" instantiation_time " + ','.join([str(e) for e in instantiation_times]))
  print(engine+" "+testcase+" invocation_time " +   ','.join([str(e) for e in invocation_times]))
  #fout_instantiation.write( ','.join([str(e) for e in instantiation_times]) )
  #fout_invocation.write(    ','.join([str(e) for e in invocation_times])    )
  fin.close()
  fout.close()
  #fout_instantiation.close()
  #fout_invocation.close()


if __name__ == "__main__":
  import sys
  if sys.argv[1] == "stderr.txt":
    get_runtimes_from_stderr_textfile("stderr.txt",sys.argv[2],sys.argv[3],sys.argv[4])


