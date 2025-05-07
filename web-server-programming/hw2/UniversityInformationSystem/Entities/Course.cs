using System;

namespace UniversityInformationSystem.Entities;

public class Course
{
    public required string Id { get; set; }
    public required string Title { get; set; }
    public required string ClassroomId { get; set; }
    public Classroom? Classroom { get; set; }

    public List<Student> Students { get; set; } = new();
}
