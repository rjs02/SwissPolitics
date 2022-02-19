#include "projections.hpp"


void computeScore(const Eigen::MatrixXi &M, Eigen::VectorXd &res, unsigned int index) {

    const unsigned int n = M.cols(); // #parties
    Eigen::VectorXd result(n); 
    Eigen::VectorXd cmp = M.col(index).cast<double>(); // cmp is the vector we compare with given by the index argument

    for(unsigned int i = 0; i < n; ++i) {
        result(i) = cmp.dot(M.col(i).cast<double>());
    }
    result /= result(index); // norm the results to interval [-1, 1]

    res = result;
}