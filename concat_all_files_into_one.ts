// This is a typescript file meant to be ran through deno: https://deno.com/

const src = './src'

// Files to exclude from concatenation
const excludeFiles = ['14_Glossary.md']

function getAllFilePaths(dir: string): Array<string> {
    const filesAndDirs = [...Deno.readDirSync(dir)]
    const dirs = filesAndDirs.filter((x) => x.isDirectory)
    const files = filesAndDirs
        .filter((x) => x.isFile)
        .filter((x) => !excludeFiles.includes(x.name))
        .map((f) => `${dir}/${f.name}`)
    const filesFromDirs = dirs.flatMap((subdir) => getAllFilePaths(`${dir}/${subdir.name}`))

    return files.concat(filesFromDirs);
}

const allFiles = getAllFilePaths(src).sort().map((f) => Deno.readTextFileSync(f));

Deno.writeTextFileSync('DND-SRD-5.2.1-RU.md', allFiles.join('\n'));
