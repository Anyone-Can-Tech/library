-- include-code.lua
-- Replace the contents of a code block with a file from disk, so the book
-- always shows the exact config readers will run.
--
-- Usage in a chapter:
--
--   ```{.yaml include="labs/06-ad-blocking/compose.yaml" filename="compose.yaml"}
--   ```
--
-- Paths are relative to the book folder (where _quarto.yml lives).

local function book_root()
  local root = quarto and quarto.project and quarto.project.directory
  return root or "."
end

function CodeBlock(block)
  local path = block.attributes["include"]
  if not path then
    return nil
  end

  local full = book_root() .. "/" .. path
  local file = io.open(full, "r")
  if not file then
    error("include-code: could not open " .. full)
  end
  local text = file:read("*a")
  file:close()

  block.text = text:gsub("\n$", "")
  block.attributes["include"] = nil
  return block
end
