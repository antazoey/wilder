using System.Collections.Generic;
using System.IO;
using Wilder.FLP;

namespace Wilder.Controllers
{
    public class FLProjectsController
    {
        readonly string _projectsDirectoryPath;

        public FLProjectsController(string projectsDirectoryPath)
        {
            _projectsDirectoryPath = projectsDirectoryPath;
        }

        public List<Project> GetProjects()
        {
            var projectsDirectory = new DirectoryInfo(_projectsDirectoryPath);
            var projectFiles = projectsDirectory.GetFiles();
            var projects = new List<Project>();
            foreach (var flpFile in projectFiles)
            {
                var project = Project.Load(flpFile.FullName);
                projects.Add(project);
            }
            return projects;
        }
    }
}
