// -----------------------------------------------------------------------------
//
// Copyright (C) The BioDynaMo Project.
// All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
//
// See the LICENSE file distributed with this work for details.
// See the NOTICE file distributed with this work for additional information
// regarding copyright ownership.
//
// -----------------------------------------------------------------------------

#ifndef CORE_DEFAULT_FORCE_H_
#define CORE_DEFAULT_FORCE_H_

#include <array>

namespace bdm {

class SimObject;

class DefaultForce {
 public:
  DefaultForce() {}
  ~DefaultForce() {}
  DefaultForce(const DefaultForce&) = delete;
  DefaultForce& operator=(const DefaultForce&) = delete;

  std::array<double, 4> GetForce(const SimObject* lhs, const SimObject* rhs);

 private:
  void ForceBetweenSpheres(const SimObject* sphere_lhs,
                           const SimObject* sphere_rhs,
                           std::array<double, 3>* result) const;

  void ForceOnACylinderFromASphere(const SimObject* cylinder,
                                   const SimObject* sphere,
                                   std::array<double, 4>* result) const;

  void ForceOnASphereFromACylinder(const SimObject* sphere,
                                   const SimObject* cylinder,
                                   std::array<double, 3>* result) const;

  void ForceBetweenCylinders(const SimObject* cylinder1,
                             const SimObject* cylinder2,
                             std::array<double, 4>* result) const;

  std::array<double, 4> ComputeForceOfASphereOnASphere(
      const std::array<double, 3>& c1, double r1,
      const std::array<double, 3>& c2, double r2) const;
};

}  // namespace bdm

#endif  // CORE_DEFAULT_FORCE_H_
