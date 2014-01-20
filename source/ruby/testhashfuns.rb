require 'openssl'

abort 'usage: ruby testhashfuns.rb'\
' repeatcount warmupcount algoname datafilename' unless ARGV.length >= 4

repeatcount, warmupcount, algoname, datafilename = ARGV

# get hash function
hashfun = case algoname
            when 'md5'
              OpenSSL::Digest::MD5.new
            when 'sha1'
              OpenSSL::Digest::SHA1.new
            when 'sha256'
              OpenSSL::Digest::SHA256.new
            when 'sha512'
              OpenSSL::Digest::SHA512.new
            else
              abort("invalid hash algorithm '#{algoname}'")
          end

#puts "hashfun #{hashfun.name}"

# read data
data = IO.binread(datafilename)

# warmup
(0..warmupcount.to_i-1).each do |i|
  hashval = hashfun.digest(data)
end

# real
(0..repeatcount.to_i-1).each_with_index do |i|
  t1 = Time.now.to_f
  hashval = hashfun.digest(data)
  elapsed = ((Time.now.to_f - t1)*1000.0).to_i
  puts "#{i} #{hashval.unpack('H*')[0]} #{elapsed}" # H msb first, h lsb first
end
