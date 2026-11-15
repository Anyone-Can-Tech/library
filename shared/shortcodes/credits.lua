-- credits.lua
-- Shortcode that drops the generated contributor credits into a chapter.
--
-- Usage at the top of a chapter:  {{< credits 06-ad-blocking >}}
--
-- The argument is the chapter's file name without .qmd. It has to be explicit
-- because PDF and EPUB builds merge every chapter into one document, so the
-- shortcode can't tell which chapter it's in on its own.
--
-- shared/scripts/credits.py runs as a Quarto pre-render step and writes
-- _credits/<chapter-file-stem>.md. Shortcodes run after pre-render, which is
-- why this is a shortcode and not a plain include.

local function stem_of(path)
  return path:match("([^/\\]+)%.qmd$") or path:match("([^/\\]+)%.[^.]+$")
end

return {
  ["credits"] = function(args, kwargs, meta)
    local stem = args[1] and pandoc.utils.stringify(args[1]) or stem_of(quarto.doc.input_file)
    local root = quarto.project.directory or "."
    local path = root .. "/_credits/" .. stem .. ".md"

    local file = io.open(path, "r")
    if not file then
      quarto.log.warning("credits: no credits file at " .. path .. ", did pre-render run?")
      return pandoc.Null()
    end
    local text = file:read("*a")
    file:close()

    return pandoc.read(text, "markdown").blocks
  end
}
