#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <fstream>
#include <Eigen/Dense>

#include "loadCSV.hpp"
#include "projections.hpp"

int main(int argc, char *argv[]) {

    if(argc > 2) {
        std::cout << "\nUsage: './projection' for single comparison to a party (interactive)"
                  << "\n   or: './projection <file>' to output all results to <file>\n\n";
        return 1;
    }

    // read in csv into matrix
    Eigen::MatrixXi parolen;
    std::vector<Vote> votes;
    std::vector<std::string> parties;
    std::string path = "../data/abst-parolen.CSV";
    
    load_csv(path, parolen, votes, parties);
    Eigen::VectorXd scores;
    
    // single comparison
    if(argc == 1) {
        unsigned int i = 0, ind;
        std::cout << "| ";
        for(auto &s : parties) {
            std::cout << i++ << " " << s << " | ";
        }
        std::cout << "\nEnter index to compute score by projection: ";
        std::cin >> ind;

        computeScore(parolen, scores, ind);

        // Output
        i = 0;
        std::cout << "---------------------------------------------\n\n"
                << "Comparing " << parties[ind] << " to:\n";
        std::cout << std::setprecision(4);
        for(auto x : scores) {
            if(i++ == ind) continue; // skip the party we compare against (avoid showing score 1.00)
            std::cout << std::fixed
                      << std::setw(7) << parties[i-1] << ": " 
                      << std::setw(8) << x << "\n";
        }
        std::cout << "\n\n";
        return 0;
    }

    // output all results to file
    std::ofstream out(argv[1]); // argv contains filename
    // header
    unsigned int n = parties.size();
    for(unsigned int i = 0; i < n; ++i) {
        out << parties[i];
        if(i != n-1) out << ",";
    }
    out << "\n";

    // compute and output results
    out << std::setprecision(4) << std::fixed;
    for(unsigned int i = 0; i < n; ++i) {
        computeScore(parolen, scores,i);
        for(unsigned int j = 0; j < n; ++j) {
            out << scores(j);
            if(j != n-1) out << ",";
        }
        if(i != n-1) out << "\n";
    }

    return 0;
}