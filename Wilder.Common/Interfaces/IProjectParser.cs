namespace Wilder.Common.Interfaces
{
    public interface IProjectParser
    {
        public IProject Parse(string projectFilePath);
    }
}