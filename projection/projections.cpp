#include "projections.hpp"


void computeScore(const Eigen::MatrixXi &M, Eigen::VectorXd &res, unsigned int index) {

    const unsigned int n = M.cols(); // #parties
    Eigen::VectorXd result(n); 
    Eigen::VectorXd cmp = M.col(index).cast<double>(); // cmp is the vector we compare with given by the index argument

    for(unsigned int i = 0; i < n; ++i) {
        result(i) = cmp.dot(M.col(i).cast<double>());
    }
    
    // norm the results to interval [-1, 1]
    result /= result(index); 
    // transform [-1, 1] to [0, 1]
    result += Eigen::VectorXd::Ones(n);
    result /= 2.;

    res = result;
}