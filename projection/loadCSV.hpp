#ifndef LOADCSV_HPP
#define LOADCSV_HPP

#include <vector>
#include <string>
#include <fstream>
#include <Eigen/Dense>

// class to store name and date for each vote
class Vote{
public:
    Vote(std::string n = "", std::string d = "9999-99-99") : name(n), date(d) {}
    std::string name;
    std::string date;
};

// read csv file from path and parse content to given arguments
void load_csv (const std::string &path, Eigen::MatrixXi &parolen, std::vector<Vote> &v, std::vector<std::string> &p);


#endif /* LOADCSV_HPP */