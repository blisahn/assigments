using System;

namespace UniversityInformationSystem.Entities;

public class Student
{
    public required string Id { get; set; }

    public required string Name { get; set; }

    public required string Email { get; set; }
    public List<Course> Courses { get; set; } = new();
}
