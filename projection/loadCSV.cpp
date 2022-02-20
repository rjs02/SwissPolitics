#include "loadCSV.hpp"
#include <iostream>

// adapted from https://stackoverflow.com/questions/34247057/how-to-read-csv-file-and-assign-to-eigen-matrix
void load_csv (const std::string &path, Eigen::MatrixXi &parolen, std::vector<Vote> &v, std::vector<std::string> &p) {
    using namespace Eigen;

    std::ifstream in(path);
    std::string line, cell;
    std::vector<int> values; // stores values in {-1, 0, 1}, will be converted to MatrixXi
    std::vector<Vote> votes; // store name and date of each vote
    std::vector<std::string> parties;
    unsigned rows = 0;
    const char delim = ',';

    // parse first row of csv (header)
    // throw away first two cols of first row
    std::getline(in, line);
    std::stringstream lineStream(line);
    std::getline(lineStream, cell, delim);
    std::getline(lineStream, cell, delim);

    // read in parties
    // result of a vote is treated like a party
    while(std::getline(lineStream, cell, delim)) {
        parties.push_back(cell);
    }

    // read in next lines
    while (std::getline(in, line)) {
        std::stringstream lineStream(line);
        std::string date, name;
        std::getline(lineStream, date, delim); 
        std::getline(lineStream, name, delim); 
        votes.emplace_back(Vote(name, date));    // add first two entries two votes vector
        
        while (std::getline(lineStream, cell, delim)) {
            values.push_back(std::stoi(cell));
        }
        ++rows;
    }

    // delete '\n' or CR (ASCII 13) at end of string of last party
    std::string s = parties[parties.size()-1];
    if (!s.empty() && (s[s.length()-1] == '\n' || s[s.length()-1] == (char)13)) {
        s.erase(s.length()-1);
    }
    parties[parties.size()-1] = s;

    // store to return data
    parolen = Map<Matrix<int, Dynamic, Dynamic, RowMajor>>(values.data(), rows, values.size()/rows);
    p = parties;
    v = votes;
}