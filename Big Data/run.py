# run.py
from job import MyJob
files = ["Novels - P4/TaleOfTwoCities.txt", "Novels - P4/Frankenstein.txt"]

for f in files:
    mr_job = MyJob(args=[f])
    print "*"*50
    with mr_job.make_runner() as runner:
        print runner._input_paths
        runner.run()
        for line in runner.stream_output():
            key, value = mr_job.parse_output_line(line)
            print key, value
        # ... etc