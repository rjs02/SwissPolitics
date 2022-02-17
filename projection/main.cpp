#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <Eigen/Dense>


class Vote{
public:
    Vote(std::string n = "", std::string d = "9999-99-99") : name(n), date(d) {}
    std::string name;
    std::string date;
};

// code from https://stackoverflow.com/questions/34247057/how-to-read-csv-file-and-assign-to-eigen-matrix
//template<typename M>
void load_csv (const std::string &path, Eigen::MatrixXi &parolen, std::vector<Vote> &v, std::vector<std::string> &p) {
    using namespace Eigen;

    std::ifstream in(path);
    std::string line, cell;
    std::vector<int> values;
    std::vector<Vote> votes;
    std::vector<std::string> parties;
    unsigned rows = 0;

    // parse first row of csv (header)
    // throw away first two cols of first row
    std::getline(in, line);
    std::stringstream lineStream(line);
    std::getline(lineStream, cell, ';');
    std::getline(lineStream, cell, ';');

    // read in parties
    // result of a vote is treated like a party
    while(std::getline(lineStream, cell, ';')) {
        parties.push_back(cell);
    }

    // read in next lines
    while (std::getline(in, line)) {
        std::stringstream lineStream(line);
        std::string date, name;
        std::getline(lineStream, date, ';'); 
        std::getline(lineStream, name, ';'); 
        votes.emplace_back(Vote(name, date));    // add first two entries two votes vector
        
        while (std::getline(lineStream, cell, ';')) {
            values.push_back(std::stoi(cell));
        }
        ++rows;
    }
    //return Map<const Matrix<typename M::Scalar, M::RowsAtCompileTime, M::ColsAtCompileTime, RowMajor>>(values.data(), rows, values.size()/rows);
    //parolen = Map<MatrixXi, ColMajor>(values.data(), rows, values.size()/rows);
    parolen = Map<Matrix<int, Dynamic, Dynamic, RowMajor>>(values.data(), rows, values.size()/rows);
    p = parties;
    v = votes;
}



int main() {

    // read in csv into matrix
    Eigen::MatrixXi parolen;
    std::vector<Vote> votes;
    std::vector<std::string> parties;
    std::string path = "../data/abst-parolen.CSV";
    
    load_csv(path, parolen, votes, parties);

    std::cout << parolen << std::endl;
    for(auto x : parties) {
        std::cout << x << " ";
    }

    for(auto x : votes) {
        std::cout << x.date << "  " << x.name << std::endl;
    }
    return 0;
}