#include <iostream>
#include <vector>
#include <string>
#include <Eigen/Dense>

#include "loadCSV.hpp"


int main() {

    // read in csv into matrix
    Eigen::MatrixXi parolen;
    std::vector<Vote> votes;
    std::vector<std::string> parties;
    std::string path = "../data/abst-parolen.CSV";
    
    load_csv(path, parolen, votes, parties);
    /*
    // test output
    for(auto x : parties) {
        std::cout << x << " ";
    }
    //std::cout << "\n";
    std::cout << parolen << "\n";
    for(auto x : votes) {
        std::cout << x.date << "  " << x.name << "\n";
    } */
    std::cout << parties[parties.size()-1] << parties[parties.size()-1] << parties[parties.size()-1];

    return 0;
}