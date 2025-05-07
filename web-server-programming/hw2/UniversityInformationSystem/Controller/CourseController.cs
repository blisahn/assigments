using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using UniversityInformationSystem.Data;
using UniversityInformationSystem.Entities;

namespace UniversityInformationSystem.Controller
{
    [Route("api/courses")]
    [ApiController]
    public class CourseController : ControllerBase
    {
        private readonly AppDbContext _context;

        public CourseController(AppDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<object>>> GetCourses()
        {
            return await _context
                .Courses.Include(c => c.Classroom) // Load Classroom details
                .Select(c => new
                {
                    c.Id,
                    c.Title,
                    Classroom = new
                    {
                        c.Classroom.Id,
                        c.Classroom.Description,
                        c.Classroom.Capacity,
                    }, // Return classroom details
                })
                .ToListAsync();
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<object>> GetCourse(string id)
        {
            var course = await _context
                .Courses.Include(c => c.Classroom)
                .Where(c => c.Id == id)
                .Select(c => new
                {
                    c.Id,
                    c.Title,
                    Classroom = new
                    {
                        c.Classroom.Id,
                        c.Classroom.Description,
                        c.Classroom.Capacity,
                    },
                })
                .FirstOrDefaultAsync();

            if (course == null)
                return NotFound();

            return course;
        }

        [HttpPost]
        public async Task<ActionResult<Course>> AddCourse(Course course)
        {
            _context.Courses.Add(course);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetCourse), new { id = course.Id }, course);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateCourse(string id, Course updatedCourse)
        {
            if (id != updatedCourse.Id)
                return BadRequest();

            var existingCourse = await _context.Courses.FindAsync(id);
            if (existingCourse == null)
                return NotFound();

            existingCourse.Title = updatedCourse.Title;
            existingCourse.ClassroomId = updatedCourse.ClassroomId;

            _context.Courses.Update(existingCourse);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteCourse(string id)
        {
            var course = await _context.Courses.FindAsync(id);
            if (course == null)
                return NotFound();

            _context.Courses.Remove(course);
            await _context.SaveChangesAsync();

            return NoContent();
        }
    }
}
