using System;

namespace UniversityInformationSystem.Entities;

public class Classroom
{
    public required string Id { get; set; }

    public string? Description { get; set; }

    public int Capacity { get; set; }

    public List<Course> Courses { get; set; } = new();
}
