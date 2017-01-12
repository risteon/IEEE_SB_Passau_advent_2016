// this is for emacs file handling -*- mode: c++; indent-tabs-mode: nil -*-
// -- BEGIN LICENSE BLOCK ----------------------------------------------
// -- END LICENSE BLOCK ------------------------------------------------
//----------------------------------------------------------------------
/*!\file
 *
 * \author  Christoph Rist <rist.christoph@gmail.com>
 * \date    2016-12-07
 *
 */
//----------------------------------------------------------------------
/***********************************
 * IEEE SB Passau Adventskalender
 * Problem 07
 */

#include <memory>
#include <iostream>
#include <iomanip>
#include <vector>
#include <array>
#include <cmath>
#include <algorithm>


using namespace std;

using Vector3D = array<double, 3>;
Vector3D operator+ (const Vector3D& a, const Vector3D& b)
{
  return {a[0] + b[0], a[1] + b[1], a[2] + b[2]};
}
Vector3D operator* (const double f, const Vector3D& a)
{
  return {f*a[0], f*a[1], f*a[2]};
}
double operator* (const Vector3D& a, const Vector3D& b)
{
  return a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
}
std::ostream& operator<< (std::ostream& stream, const Vector3D& v)
{
  stream <<setprecision(5) <<v[0] <<" " <<v[1] <<" " <<v[2];
  return stream;
}
Vector3D norm(const Vector3D& v)
{
  const double len = sqrt(v*v);
  return (1.0/len) * v;
}

int main(int argc, char* argv[])
{
  Vector3D x{};
  Vector3D v{};
  cin >> x[0] >> x[1] >> x[2];
  cin >> v[0] >> v[1] >> v[2];

  const double a = v[0]*v[0] + v[1]*v[1];
  const double b = 2*x[0]*v[0] + 2*x[1]*v[1] - 100*v[2];
  const double c = x[0]*x[0] + x[1]*x[1] - 100*x[2];

  const double under_root = b*b - 4*a*c;
  if (under_root < 0.0)
  {
    cout <<"Error!" <<endl;
    return 0;
  }

  vector<double> t{};
  t.push_back((-b + sqrt(under_root)) / (2*a));
  t.push_back((-b - sqrt(under_root)) / (2*a));

  // smallest positive t is the first one to hit surface
  // discard negatives
  if (t.front() < 0.0)
  {
    t.erase(t.begin());
  }
  if (t.back() < 0.0)
  {
    t.pop_back();
  }
  if (t.empty())
  {
    cout <<"Error!" <<endl;
    return 0;
  }

  // Intersection
  const double pos = *min_element(t.cbegin(), t.cend());
  const Vector3D intersection = x + pos*v;
  // normal vector
  const Vector3D normal = {-0.02 * intersection[0], -0.02 * intersection[1], 1.0};
  // projection
  const Vector3D direction = -1.0 * v;
  const Vector3D projection = ((direction * normal) / (normal * normal)) * normal;
  const Vector3D emission = 2.0 * projection + v;
  const Vector3D normed_emission = norm(emission);

  cout <<fixed <<setprecision(5) <<intersection <<" " <<normed_emission <<endl;

  return 0;
}
