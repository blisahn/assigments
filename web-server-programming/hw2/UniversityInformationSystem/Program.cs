using Microsoft.EntityFrameworkCore;
using UniversityInformationSystem.Data;
using UniversityInformationSystem.Entities;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
// builder.Services.AddOpenApi();
builder.Services.AddDbContext<AppDbContext>(options => options.UseInMemoryDatabase("TestDatabase"));
builder.Services.AddControllers();

var app = builder.Build();

using var scope = app.Services.CreateScope();
var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

// Check if data exists to prevent duplicate seeding
if (!context.Students.Any())
{
    var course1 = new Course
    {
        Id = "BIM308",
        Title = "Web Server Programming",
        ClassroomId = "B6",
    };

    var course2 = new Course
    {
        Id = "BIM439",
        Title = "Computer Networks",
        ClassroomId = "B6",
    };

    var student = new Student
    {
        Id = "",
        Name = " ",
        Email = "",
        Courses = [course1, course2], // Assign courses to student
    };

    var classroom = new Classroom
    {
        Id = "B6",
        Description = "Computer Engineering Ground Floor",
        Capacity = 60,
        Courses = [course1, course2],
    };

    // Add entities to the context
    context.Students.Add(student);
    context.Courses.AddRange(course1, course2);
    context.Classrooms.Add(classroom);

    await context.SaveChangesAsync();
}

app.MapControllers();
app.Run();
