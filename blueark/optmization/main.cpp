#include <iostream>
#include <cassert>
#include <CGAL/QP_models.h>
#include <CGAL/QP_functions.h>
#include <CGAL/Gmpq.h>
#include <vector>
#include <string>

typedef CGAL::Gmpq ET;

typedef CGAL::Quadratic_program<double> Program;
typedef CGAL::Quadratic_program_solution<ET> Solution;

using std::cin;
using std::cout;

int main(){
  int n, m;

  std::cin >> n >> m;
  cout << m << " " << n << std::endl;
  std::vector<std::string> names(n);
  Program lp(CGAL::SMALLER, true, 0, false, 0);
  double a, b, c, eq;

  for(int var = 0; var < n; ++var){
    // a <= var <= b
    cin >> a >> b >> names[var] >> c;

    lp.set_c(var, -c);
    if(a > 0){
      lp.set_l(var, true, a);
    }
    if(b >= 0){
      lp.set_u(var, true, b);
    }
  }

  // each of the following m lines is:
  // a[i][0] ... a[i][n-1] <= b[i]
  // where "<=" is an integer, 0 if equal
  cout << m << " " << n << std::endl;
  for(int constraint = 0; constraint < m; ++constraint){
    for(int variable = 0; variable < n; ++variable){
      cin >> a;
      lp.set_a(variable, constraint, a);
    }
    cin >> eq >> b;
    cout << eq << " " << b << std::endl;
    lp.set_b(constraint, b);
    if(eq == 0){
      lp.set_r(constraint, CGAL::EQUAL);
    }
  }

  Solution s = CGAL::solve_linear_program(lp, ET());
  if(!s.solves_linear_program(lp) || s.status() == CGAL::QP_INFEASIBLE)
    std::cout << "no\n";
  else{
    ET ans = s.objective_value().numerator() / s.objective_value().denominator();
    std::cout << -CGAL::to_double(s.objective_value()) << "\n";
  }
  CGAL::Quadratic_program_solution<ET>::Variable_value_iterator 
    opt = s.variable_values_begin();

    cout << "hello\n";
  for(int i = 0; i < n; ++i){
    cout << names[i] << "," << CGAL::to_double(*(opt + i)) << "\n";
  }
  return 0;
}
