import sox

file = 'data/stereo-test.mp3'
tmpfile = 'tmp.mp3'

# create transformer
tfm = sox.Transformer()

tfm.swap()


# create an output file.
tfm.build_file(file, tmpfile)

# get the output in-memory as a numpy array
# by default the sample rate will be the same as the input file
# asrray_out = tfm.build_array(input_filepath=file)

# print(array_out)
