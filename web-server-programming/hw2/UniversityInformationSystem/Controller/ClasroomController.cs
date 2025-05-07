using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using UniversityInformationSystem.Data;
using UniversityInformationSystem.Entities;

namespace UniversityInformationSystem.Controller
{
    [Route("api/classrooms")]
    [ApiController]
    public class ClasroomController : ControllerBase
    {
        private readonly AppDbContext _context;

        public ClasroomController(AppDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<object>>> GetClassrooms()
        {
            return await _context
                .Classrooms.Include(c => c.Courses) // Load courses assigned to the classroom
                .Select(c => new
                {
                    c.Id,
                    c.Description,
                    c.Capacity,
                    Courses = c.Courses.Select(cr => new { cr.Id, cr.Title }).ToList(), // Return course details
                })
                .ToListAsync();
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<object>> GetClassroom(string id)
        {
            var classroom = await _context
                .Classrooms.Include(c => c.Courses)
                .Where(c => c.Id == id)
                .Select(c => new
                {
                    c.Id,
                    c.Description,
                    c.Capacity,
                    Courses = c.Courses.Select(cr => new { cr.Id, cr.Title }).ToList(),
                })
                .FirstOrDefaultAsync();

            if (classroom == null)
                return NotFound();

            return classroom;
        }
    }
}
