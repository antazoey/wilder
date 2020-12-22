using System;
using Wilder.Controllers;
using Wilder.Projects;

namespace Wilder
{
    class MainClass
    {
        public static void Main(string[] args)
        {
            var core = new Core();
            core.ProjectParser.Parse("")
            // var projects = controller.GetProjects();
            // var index = 1;
            // Console.WriteLine($"You have {projects.Count} projects:");
            // foreach (var project in projects)
            // {
            //     var projectString = $"{index}: '{project.Title}' by {project.Author}.";
            //     Console.WriteLine(projectString);
            //     Console.WriteLine(project.Genre);
            //     index += 1;
            // }
        }
    }
}
