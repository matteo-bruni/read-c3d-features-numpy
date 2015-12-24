import matlab.engine
import c3d_converter_bin_numpy
import numpy as np
import argparse

def convert_matlab_array_to_numpy(matlab_array):
    np_a = np.array(matlab_array._data.tolist())
    np_a = np_a.reshape(matlab_array.size).transpose()
    return np_a


def main(args):

    print "starting matlab engine"
    eng = matlab.engine.start_matlab()

    paths = ['binary/000000.fc6-1', 'binary/000000.fc7-1', 'binary/000016.fc6-1', 'binary/000016.fc7-1']

    for path in paths:

        print "File.. {}".format(path)

        print "\treading with matlab .."
        matlab_header, matlab_data = eng.read_binary_blob(path, nargout=2)

        print "\theader", matlab_header
        print "\tdata", matlab_data

        np_matlab_data = convert_matlab_array_to_numpy(matlab_data)
        print "\t\tsum:  ", np_matlab_data.sum()


        print "\treading with python"
        header, data =  c3d_converter_bin_numpy.read_binary_fc(path)

        print "\tHEADER: \tnum, chanel, length, height, width.\n\t\t", header
        print "\tDATA:   \tshape:\t", data.shape
        print "\t\t", data
        print "\t\tsum:  ", data.sum()

        print "\tchecking allclose()"

        # print np_matlab_data.shape
        # print data[:,np.newaxis].shape  #make same shape
        print np.allclose(np_matlab_data, data[:,np.newaxis])


def get_parser():
    parser = argparse.ArgumentParser(description="Check if numpy scripts generate the same matlab vector")
    return parser

if __name__ == '__main__':
    parser = get_parser()
    main(parser.parse_args())



