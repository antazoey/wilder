using System.Collections.Generic;
using System.IO;
using System.Linq;
using Wilder.FLP;

namespace Wilder.Controllers
{
    public class FLProjectsController
    {
        private readonly string _projectsDirectoryPath;

        public FLProjectsController(string projectsDirectoryPath)
        {
            _projectsDirectoryPath = projectsDirectoryPath;
        }

        public List<Project> GetProjects()
        {
            var projectsDirectory = new DirectoryInfo(_projectsDirectoryPath);
            var projectFiles = projectsDirectory.GetFiles();
            return projectFiles.Select(flpFile => Project.Load(flpFile.FullName)).ToList();
        }
    }
}
