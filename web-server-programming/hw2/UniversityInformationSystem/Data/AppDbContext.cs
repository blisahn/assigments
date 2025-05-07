using System;
using Microsoft.EntityFrameworkCore;
using UniversityInformationSystem.Entities;

namespace UniversityInformationSystem.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options) { }

    public DbSet<Student> Students { get; set; }
    public DbSet<Course> Courses { get; set; }
    public DbSet<Classroom> Classrooms { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Many-to-Many: Student <-> Course
        modelBuilder
            .Entity<Student>()
            .HasMany(s => s.Courses)
            .WithMany(c => c.Students)
            .UsingEntity(j => j.ToTable("StudentCourse"));

        // One-to-Many: Course <-> Classroom
        modelBuilder
            .Entity<Course>()
            .HasOne(c => c.Classroom)
            .WithMany(cl => cl.Courses)
            .HasForeignKey(c => c.ClassroomId);
    }
}
